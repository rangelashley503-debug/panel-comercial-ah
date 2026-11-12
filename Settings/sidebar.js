document.addEventListener('DOMContentLoaded', () => {
    // 1. Detectar el rol activo desde la URL (?rol=...) o localStorage (por defecto 'admin')
    const params = new URLSearchParams(window.location.search);
    const rolActual = params.get('rol') || localStorage.getItem('userRole') || 'admin';
    localStorage.setItem('userRole', rolActual);

    // 2. Rutas exactas relativas desde cualquier subcarpeta hacia la raíz de "app comercial"
    const rutasPaginas = {
        catalogo: '../Catalogo de productos- H/catalogo.html',
        inventario: '../Inventario y existencias-H/inventario.html',
        administracion: '../Administración y supervisión-H/admi.html',
        clientes: '../Clientes y cuentas comerciales - K/Clientes.html',
        pedidos: '../Gestión de pedidos y cotizaciones - K/Pedidos.html',
        pagos: '../Pagos, reportes y panel - K/Pagos.html',
        surtido: '../Surtido de almacén y logística - K/Surtido.html',
        mostrador: '../Ventas de mostrador-H/ventas_mostrador.html'
    };

    // 3. Detectar qué pantalla está abierta actualmente para iluminar su botón en terracota
    const rutaActual = decodeURIComponent(window.location.pathname).toLowerCase();

    function esPaginaActiva(seccion) {
        if (seccion === 'catalogo') return rutaActual.includes('catalogo.html');
        if (seccion === 'inventario') return rutaActual.includes('inventario.html') || rutaActual.includes('agregar_inventario.html');
        if (seccion === 'administracion') return rutaActual.includes('admi.html');
        if (seccion === 'clientes') return rutaActual.includes('clientes.html') || rutaActual.includes('registrar nueva cuenta comercial.html');
        if (seccion === 'pedidos') return rutaActual.includes('pedidos.html');
        if (seccion === 'pagos') return rutaActual.includes('pagos.html');
        if (seccion === 'surtido') return rutaActual.includes('surtido.html');
        if (seccion === 'mostrador') return rutaActual.includes('ventas_mostrador.html');
        return false;
    }

    // 4. Banco de Íconos SVG
    const iconos = {
        catalogo: `<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 11V7a4 4 0 0 0-8 0v4"/><path d="M5 9h14l1 12H4L5 9Z"/></svg>`,
        inventario: `<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="2"/><path d="M9 14h6M9 18h6"/></svg>`,
        administracion: `<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 14.93V17a1 1 0 0 1-2 0v-.07A7 7 0 0 1 5.07 11H5a1 1 0 0 1 0-2h.07A7 7 0 0 1 11 5.07V5a1 1 0 0 1 2 0v.07A7 7 0 0 1 18.93 11H19a1 1 0 0 1 0 2h-.07A7 7 0 0 1 13 16.93z"/><circle cx="12" cy="12" r="2"/></svg>`,
        clientes: `<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
        pedidos: `<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>`,
        pagos: `<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/><circle cx="7" cy="15" r="1"/></svg>`,
        surtido: `<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13" rx="1"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>`,
        mostrador: `<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3h18v4H3z"/><path d="M4 7v13a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V7"/><path d="M10 11h4"/><path d="M9 15h6"/></svg>`
    };

    // 5. Permisos por rol según tus especificaciones
    const configuracionRoles = {
        // ADMINISTRADOR: catalogo, inventario, administracion, clientes, pedidos, pagos, surtido, mostrador
        admin: {
            tituloHeader: "Administrador",
            badgeHeader: "A",
            avatar: "RV",
            nombreUsuario: "Ray Vázquez",
            cargo: "Administrador",
            opciones: [
                { id: "catalogo", nombre: "Catálogo" },
                { id: "inventario", nombre: "Inventario" },
                { id: "administracion", nombre: "Administración" },
                { id: "clientes", nombre: "Clientes" },
                { id: "pedidos", nombre: "Pedidos" },
                { id: "pagos", nombre: "Pagos" },
                { id: "surtido", nombre: "Surtido" },
                { id: "mostrador", nombre: "Mostrador" }
            ]
        },

        // VENDEDOR: catalogo, inventario, clientes, pedidos
        vendedor: {
            tituloHeader: "Ventas",
            badgeHeader: "V",
            avatar: "VN",
            nombreUsuario: "Carlos Morales",
            cargo: "Agente de Ventas",
            opciones: [
                { id: "catalogo", nombre: "Catálogo" },
                { id: "inventario", nombre: "Inventario" },
                { id: "clientes", nombre: "Clientes" },
                { id: "pedidos", nombre: "Pedidos" }
            ]
        },

        // ALMACÉN: inventario, catalogo
        almacen: {
            tituloHeader: "Almacén",
            badgeHeader: "AL",
            avatar: "AL",
            nombreUsuario: "Equipo Almacén",
            cargo: "Logística y Stock",
            opciones: [
                { id: "inventario", nombre: "Inventario" },
                { id: "catalogo", nombre: "Catálogo" }
            ]
        },

        // CLIENTE: catalogo, pedidos
        cliente: {
            tituloHeader: "Cliente",
            badgeHeader: "C",
            avatar: "CL",
            nombreUsuario: "Nombre Cliente",
            cargo: "Tienda Local",
            opciones: [
                { id: "catalogo", nombre: "Catálogo" },
                { id: "pedidos", nombre: "Pedidos" }
            ]
        }
    };

    const rolData = configuracionRoles[rolActual] || configuracionRoles.admin;

    // 6. Actualizar textos del perfil y cabecera móvil
    const headerTitle = document.getElementById('sidebarHeaderTitle');
    const badgeIcon = document.getElementById('userBadgeIcon');
    const avatarText = document.getElementById('userAvatarText');
    const nameText = document.getElementById('userNameText');
    const roleText = document.getElementById('userRoleText');
    const mobileRoleTitle = document.getElementById('mobileRoleTitle');

    if (headerTitle) headerTitle.textContent = rolData.tituloHeader;
    if (badgeIcon) badgeIcon.textContent = rolData.badgeHeader;
    if (avatarText) avatarText.textContent = rolData.avatar;
    if (nameText) nameText.textContent = rolData.nombreUsuario;
    if (roleText) roleText.textContent = rolData.cargo;
    if (mobileRoleTitle) mobileRoleTitle.textContent = rolData.tituloHeader;

    // 7. Renderizar botones (<button>) dinámicos en el sidebar y conectar eventos de redirección
    const sidebarNav = document.getElementById('sidebarNav');
    if (sidebarNav) {
        sidebarNav.innerHTML = rolData.opciones.map(op => {
            const activo = esPaginaActiva(op.id);
            return `
                <button
                    type="button"
                    data-section="${op.id}"
                    class="sidebar-nav-btn w-full flex items-center gap-4 px-4 py-3 rounded-xl font-medium text-sm transition-all duration-200 ${
                        activo
                            ? 'active bg-brand-terracotta text-white shadow-md shadow-brand-terracotta/20'
                            : 'text-gray-300 hover:bg-white/10 hover:text-white'
                    }"
                    ${activo ? 'aria-current="page"' : ''}
                >
                    <span class="shrink-0">${iconos[op.id] || ''}</span>
                    <span class="sidebar-label whitespace-nowrap">${op.nombre}</span>
                </button>
            `;
        }).join('');

        // Redirección al hacer clic en cada botón
        sidebarNav.querySelectorAll('.sidebar-nav-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const seccion = btn.getAttribute('data-section');
                const destino = rutasPaginas[seccion];
                if (destino) {
                    window.location.href = `${destino}?rol=${rolActual}`;
                }
            });
        });
    }

    // 8. Control de colapsar en escritorio y abrir/cerrar en móvil
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleSidebar');
    const openMobileBtn = document.getElementById('openMobileSidebar');
    const sidebarBackdrop = document.getElementById('sidebarBackdrop');

    function cerrarSidebarMovil() {
        if (!sidebar) return;
        sidebar.classList.remove('mobile-open');
        if (sidebarBackdrop) {
            sidebarBackdrop.classList.remove('opacity-100', 'pointer-events-auto');
            sidebarBackdrop.classList.add('opacity-0', 'pointer-events-none');
        }
    }

    if (openMobileBtn && sidebar) {
        openMobileBtn.addEventListener('click', () => {
            sidebar.classList.add('mobile-open');
            if (sidebarBackdrop) {
                sidebarBackdrop.classList.remove('opacity-0', 'pointer-events-none');
                sidebarBackdrop.classList.add('opacity-100', 'pointer-events-auto');
            }
        });
    }

    if (sidebarBackdrop) {
        sidebarBackdrop.addEventListener('click', cerrarSidebarMovil);
    }

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', () => {
            if (window.innerWidth < 1024) {
                cerrarSidebarMovil();
            } else {
                sidebar.classList.toggle('is-collapsed');
            }
        });
    }
});