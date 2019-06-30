# Log

## database-controller
### 概要
env_loggerでワンライナーでjsonのログを吐くようにする

severityも指定する．

```json
{
    "severity": "INFO",
    "content": {
        "user": {
            "id": "uuid4",
            "name": "hoge"
        }
    },
}
```