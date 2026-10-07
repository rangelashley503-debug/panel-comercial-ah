tailwind.config = {
theme: {
    extend: {
    colors: {
        // Paleta base
        brand: {
        navy: '#1A3A68',
        terracotta: '#D83816',
        amber: '#F09D25',
        cream: '#FCD090',
        cyan: '#07A6D8',
        },
        // Variaciones hover
        'brand-hover': {
        terracotta: '#B52A0F',
        amber: '#D88210',
        cyan: '#0585AD',
        },
        // Superficies y fondos
        surface: {
        app: '#F9F9FB',
        card: '#FFFFFF',
        subtle: '#FEF3E2',
        dark: '#1A3A68',
        },
        // Tipografía
        content: {
        heading: '#1A3A68',
        body: '#2D3748',
        muted: '#718096',
        },
        // Tablas y bordes
        border: {
        subtle: '#E2E8F0',
        },
        table: {
        zebra: '#FEF8F0',
        hover: '#EBF5FA',
        },
        // Alertas y estados
        status: {
        error: { bg: '#FDE8E8', text: '#D83816' },
        warning: { bg: '#FEF3C7', text: '#F09D25' },
        success: { bg: '#DEF7EC', text: '#03543F' },
        info: { bg: '#E1F5FE', text: '#07A6D8' },
        },
    },
    },
},
};