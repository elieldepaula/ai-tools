# Avoid Heavy Observers

This is a HARD RULE in this project. Observers MUST be lightweight. They dispatch or delegate work; they do not perform heavy logic.

## Why

- Observers run synchronously inside the main request lifecycle. Slow observers slow down every request that triggers them.
- Heavy work in observers blocks checkout, catalog pages and admin operations, causing timeouts and user-facing delays.
- Observers are hard to retry: if the job fails midway, the transaction is already committed.

## Forbidden patterns

```php
// FORBIDDEN — heavy work inside an observer
class SendOrderConfirmation implements ObserverInterface
{
    public function execute(Observer $observer): void
    {
        $order = $observer->getEvent()->getOrder();
        $this->pdf->generateAndSend($order);      // slow
        $this->erp->push($order->getData());      // slow network call
        $this->indexer->reindexAll();              // heavy
    }
}
```

## Correct pattern: delegate to a service + message queue

```php
// Observer stays thin
class OrderSubmittedObserver implements ObserverInterface
{
    public function __construct(
        private readonly OrderSubmittedHandler $handler,
    ) {
    }

    public function execute(Observer $observer): void
    {
        $this->handler->dispatch(
            $observer->getEvent()->getOrder()
        );
    }
}

// Handler publishes to a queue
final class OrderSubmittedHandler
{
    public function dispatch(OrderInterface $order): void
    {
        $this->messageManager->send(
            'sales.order.submitted',
            $this->serializer->serialize(['order_id' => $order->getId()])
        );
    }
}
```

A consumer (`queue_consumer.xml`) processes the message asynchronously and can retry on failure.

## Rules

- Observers MUST NOT contain business logic — they call a service/use case and return.
- Any operation taking more than ~50ms (HTTP calls, PDF, email, reindex, bulk DB) MUST go to a message queue or a cron job.
- Observers MUST NOT reindex, flush cache, or run long loops synchronously.
- Long-running processes: use cron jobs or queue consumers.
- Email/notification sending: use the queue (`Magento\Sales\Model\Order\Email\Sender` publishes by default) — do not send inline.
- If the queue is unavailable, log and let the consumer retry; never block the request.

## Enforcement

- Code review flags observers containing loops, network calls, email/PDF generation or reindexing.
- Violations are treated as high/critical issues.
- Static analysis and profiling (Blackfire/Telescope-like traces) verify observer execution time stays within budget.
