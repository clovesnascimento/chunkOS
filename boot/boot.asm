; CHUNK OS Bootloader (Stub)
; Minimal x86_64 bootloader to transition to protected mode

[BITS 16]
[ORG 0x7C00]

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00

    ; Print greeting
    mov si, msg_hello
    call print_string

    ; Transition to 32-bit (Stub)
    ; Real bootloader would load kernel here
    jmp $

print_string:
    lodsb
    or al, al
    jz .done
    mov ah, 0x0E
    int 0x10
    jmp print_string
.done:
    ret

msg_hello db 'CHUNK OS Booting...', 0x0D, 0x0A, 0

times 510-($-$$) db 0
dw 0xAA55
