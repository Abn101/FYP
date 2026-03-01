// Logout utility for all dashboards
function setupLogoutButton() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            localStorage.removeItem('authUser');
            localStorage.removeItem('lg_client_name');
            localStorage.removeItem('lg_lawyer_name');
            window.location.href = 'login-selection.html';
        });
    }
}
// Simple frontend auth utility
// Usage: authCheck({ requiredRole: 'lawyer' })

function authCheck({ requiredRole }) {
    const user = JSON.parse(localStorage.getItem('authUser') || 'null');
    if (!user || !user.role) {
        window.location.href = 'login-selection.html';
        return;
    }
    if (requiredRole && user.role !== requiredRole) {
        // Redirect to their dashboard
        if (user.role === 'lawyer') {
            window.location.href = 'Ldash.html';
        } else if (user.role === 'client') {
            window.location.href = 'client-dashboard.html';
        } else if (user.role === 'admin') {
            window.location.href = 'admin-dashboard.html';
        } else {
            window.location.href = 'login-selection.html';
        }
    }
}

// Example: call authCheck({ requiredRole: 'lawyer' }) at the top of lawyer pages
