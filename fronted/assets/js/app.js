const API_URL = "http://localhost:3000/api";

/* LOGIN */
async function loginUser(e){
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${API_URL}/auth/login`,{
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({ email,password })
    });

    const data = await res.json();

    if(res.ok){
        localStorage.setItem("token", data.token);
        window.location.href="dashboard.html";
    }else{
        showToast(data.message);
    }
}

document.addEventListener("DOMContentLoaded", function () {

    const togglePassword = document.getElementById("togglePassword");
    const passwordInput = document.getElementById("password");

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener("click", function () {

            const type = passwordInput.type === "password" ? "text" : "password";
            passwordInput.type = type;

            this.classList.toggle("fa-eye");
            this.classList.toggle("fa-eye-slash");
        });
    }

});

/* REGISTER */
async function registerUser(e){
    e.preventDefault();

    const nombre = document.getElementById("nombre").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${API_URL}/auth/register`,{
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({ nombre,email,password })
    });

    const data = await res.json();
    showToast(data.message);

    if(res.ok){
        window.location.href="login.html";
    }
}

/* LOTES */
async function cargarLotes(){
    const res = await fetch(`${API_URL}/lotes`);
    const lotes = await res.json();

    const tabla = document.getElementById("tablaLotes");
    tabla.innerHTML="";

    lotes.forEach(lote=>{
        tabla.innerHTML+=`
        <tr>
            <td>${lote.area} m²</td>
            <td>${lote.ubicacion}</td>
            <td>$${lote.valor}</td>
            <td class="status-${lote.estado.toLowerCase()}">${lote.estado}</td>
            <td><button onclick="showToast('Compra simulada')">Comprar</button></td>
        </tr>
        `;
    });
}

/* FILTRO */
function filtrarLotes(){
    const filtro=document.getElementById("filtroEstado").value;
    const filas=document.querySelectorAll("#tablaLotes tr");

    filas.forEach(f=>{
        const estado=f.children[3].innerText;
        f.style.display=(!filtro||estado===filtro)?"":"none";
    });
}

/* TOAST */
function showToast(msg){
    const toast=document.createElement("div");
    toast.className="toast";
    toast.innerText=msg;
    document.body.appendChild(toast);

    setTimeout(()=>toast.remove(),3000);
}

function logout(){
    localStorage.removeItem("token");
    window.location.href="login.html";
}