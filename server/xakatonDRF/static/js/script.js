document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    
    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('hidden');
        
        // Меняем иконку
        const icon = this.querySelector('i');
        if (sidebar.classList.contains('hidden')) {
            icon.classList.replace('fa-bars', 'fa-arrow-right');
        } else {
            icon.classList.replace('fa-arrow-right', 'fa-bars');
        }
    });
});

