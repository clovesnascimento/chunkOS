/* CHUNK OS Linker Script */
/* CNGSM — Cloves Nascimento */

ENTRY(_start)

SECTIONS
{
    . = 0x1000;
    
    .text : {
        *(.text)
        *(.text.*)
    }
    
    .rodata : {
        *(.rodata)
        *(.rodata.*)
    }
    
    .data : {
        *(.data)
        *(.data.*)
    }
    
    .bss : {
        *(.bss)
        *(.bss.*)
    }
    
    /* Seção especial para pesos da LLM */
    .weights : {
        _weights_start = .;
        *(.weights)
        _weights_end = .;
    }
    
    /* Seção para cache KV inicial */
    .kv_cache : {
        _kv_cache_start = .;
        *(.kv_cache)
        _kv_cache_end = .;
    }
}
