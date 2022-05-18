import JWTPars from "./JWTPars";
export default function isAuthenticated(){
    /// This is a helper function that returns true if the user is authenticated.
    let exp;
    exp = localStorage.getItem("token") ? JWTPars(localStorage.getItem("token")).exp : null
    const excludedRoutes = ['/NotFound', '/auth/login', '/auth/logout', '/auth/register', '/auth/forgot-password', '/auth/reset-password'];
    if(Date.now() >= exp*1000 && !excludedRoutes.includes(window.location.pathname)){
        localStorage.removeItem("token");
        window.location.href = '/auth/login'
    }
    else {
        
    }
}
