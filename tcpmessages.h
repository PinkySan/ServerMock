#ifndef TCPMESSAGES_H
#define TCPMESSAGES_H

#include <stdint.h>

// Portable packed struct macros
#if defined(_MSC_VER)
    #define PACKED_STRUCT(definition) __pragma(pack(push, 1)) definition __pragma(pack(pop))
#else
    #define PACKED_STRUCT(definition) definition __attribute__((packed))
#endif

#define STARTBIT 0xABCD

enum message_id {
    MSG_ID_HELLO = 1,
    MSG_ID_GOODBYE = 2,
    MSG_ID_MEASUREMENT = 3,
    // Add more message IDs as needed
};

PACKED_STRUCT(
struct hello {
    uint32_t value;
};
)

PACKED_STRUCT(
struct goodbye {
    char message[256];
};
)

PACKED_STRUCT(
struct measurement {
    float temperature;
    float humidity;
};
)

PACKED_STRUCT(
struct Message {
    uint32_t startbit;
    uint32_t message_id;
    uint32_t payload_length;
    uint32_t header_checksum;
    char payload[256];
};
)

#endif // TCPMESSAGES_H
