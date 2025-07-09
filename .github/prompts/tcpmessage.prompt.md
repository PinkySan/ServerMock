---
mode: edit
description: TCP message format specification
---

# TCP messages

* All messages will be specified in a c compatible format
* The C-compatible format contains of
    * A fixed-size header
    * A variable-size payload
* The header contains the following fields
    * `u32` - A Startbit, which is always 0xABCD
    * `u32` - The message id
    * `u32` - The length of the payload
    * `u32` - The checksum of the header
* The payload contains the actual message
* The checksum is the sum of all bytes in the header, modulo 256
* Every message is defined by a message id
* The server should be able to handle multiple message ids
* The c-style messages must always be packed struct with no padding

# Example message

```c
#include <stdint.h>

enum message_id {
    MSG_ID_HELLO = 1,
    MSG_ID_GOODBYE = 2,
    // Add more message IDs as needed
};
struct __attribute__((packed)) hello {
    uint32_t value;
};

struct __attribute__((packed)) goodbye {
    char message[256];
};
```

# Example tcp message

```c
#include <stdint.h>

struct __attribute__((packed)) Message {
    uint32_t startbit;
    uint32_t message_id;
    uint32_t payload_length;
    uint32_t header_checksum;
    char payload[256];
};
```
