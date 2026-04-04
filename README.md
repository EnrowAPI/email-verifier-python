# Email Verifier - Python Library

[![PyPI version](https://img.shields.io/pypi/v/email-verifier.svg)](https://pypi.org/project/email-verifier/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Verify email addresses for deliverability, catch-all detection, and inbox status. Clean your email lists before sending to reduce bounces and protect your sender reputation.

Powered by [Enrow](https://enrow.io) -- works on catch-all domains, only charged for verified results.

## Installation

```bash
pip install email-verifier
```

Requires Python 3.8+. Only dependency: `httpx`.

## Simple Usage

```python
from enrow_email_verifier import verify_email, get_verification_result

verification = verify_email(
    api_key="your_api_key",
    email="tcook@apple.com",
)

result = get_verification_result("your_api_key", verification["id"])

print(result["qualification"])  # valid
print(result["isDeliverable"])  # True
print(result["isCatchAll"])     # False
```

`verify_email` returns a verification ID. The verification runs asynchronously -- call `get_verification_result` to retrieve the result once it's ready. You can also pass a `webhook` URL to get notified automatically.

## Bulk verification

```python
from enrow_email_verifier import verify_emails, get_verification_results

batch = verify_emails(
    api_key="your_api_key",
    emails=[
        "tcook@apple.com",
        "satya@microsoft.com",
        "jensen@nvidia.com",
    ],
)

# batch["batchId"], batch["total"], batch["status"]

results = get_verification_results("your_api_key", batch["batchId"])
# results["results"] -- list of verification result dicts
```

Up to 5,000 verifications per batch. Pass a `webhook` URL to get notified when the batch completes.

## Error handling

```python
try:
    verify_email(api_key="bad_key", email="test@test.com")
except Exception as e:
    # str(e) contains the API error description
    # Common errors:
    # - "Invalid or missing API key" (401)
    # - "Your credit balance is insufficient." (402)
    # - "Rate limit exceeded" (429)
    print(e)
```

## Getting an API key

Register at [app.enrow.io](https://app.enrow.io) to get your API key. You get **50 free credits** (= 200 verifications) with no credit card required.

Each verification costs **0.25 credits**. Paid plans start at **$17/mo** up to **$497/mo**. See [pricing](https://enrow.io/pricing).

## Documentation

- [Enrow API documentation](https://docs.enrow.io)
- [Full Enrow SDK](https://github.com/enrow/enrow-python) -- includes email finder, phone finder, reverse email lookup, and more

## License

MIT -- see [LICENSE](LICENSE) for details.
