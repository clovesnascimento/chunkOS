; CHUNK OS Bootloader
; CNGSM — Cloves Nascimento
; Boot assembly para sistemas x86_64 (simulação)

section .text
global _start

_start:
    ; Inicializa segmentos
    mov ax, 0x07C0
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    
    ; Configura pilha
    mov ax, 0x9000
    mov ss, ax
    mov sp, 0xFFFF
    
    ; Mostra banner
    mov si, boot_msg
    call print_string
    
    ; Carrega kernel do CHUNK
    mov si, loading_msg
    call print_string
    
    ; Jump para o kernel
    jmp 0x1000:0x0000

print_string:
    lodsb
    or al, al
    jz .done
    mov ah, 0x0E
    int 0x10
    jmp print_string
.done:
    ret

; Dados
boot_msg db 'CHUNK OS - Cognitive Neural Kernel', 0x0D, 0x0A, 0
loading_msg db 'Loading CHUNK kernel...', 0x0D, 0x0A, 0

; Padding para 512 bytes (boot sector)
times 510 - ($ - $$) db 0
dw 0xAA55
