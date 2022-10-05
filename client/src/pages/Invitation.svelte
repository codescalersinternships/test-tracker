<script>
    import axios from '../healpers/axios'
    import Modal from "../components/ui/Alert.svelte";
    export let data;

    const urlParams = new URLSearchParams(window.location.search);
    let signature = urlParams.get('signature');
    async function RegisterApi(){
        const password1 = document.getElementById('password1').value;
        const password2 = document.getElementById('password2').value;
        if (password1 != password2) {
            alert("Passwords do not match");
            return;
        }
        try {
            const response = await axios.put(`members/set_password/?signature=${signature}`, {password:password1})
        if (response.status === 201) { await InviteSuccess() }} 
        catch(err) {
            console.log(err.response);
        }
    }
    async function InviteSuccess() {
        try {
            const success = await axios.put(`auth/invitation/?signature=${signature}`, data)
        if (success.status === 200) { window.location.href = '/' }} 
        catch(err) {
            console.log(err.response.data.error);
        }
    }
</script>

<svelte:head>
    <title>Test-Tracker | Register</title>
</svelte:head>

<section class="vh-100" style="background-color: #eee;">
    <div class="container h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-lg-12 col-xl-11">
          <div class="card text-black" style="border-radius: 25px;">
            <div class="card-body p-md-5">
              <div class="row justify-content-center">
                <div class="col-md-10 col-lg-6 col-xl-5 order-2 order-lg-1">
                  <p class="text-center h1 fw-bold mb-5 mx-1 mx-md-4 mt-4">Sign up</p>
                  <form class="mx-1 mx-md-4">
                    <div class="mb-3">
                      {#if data.first_name}
                        <p class="h5 text-center">
                          Hello <span class="text-primary">{data.first_name} {data.last_name}</span>
                        </p>
                      {/if}
                    </div>
                    <div class="d-flex flex-row align-items-center mb-4">
                      <i class="fas fa-lock fa-lg me-3 fa-fw"></i>
                      <div class="form-outline flex-fill mb-0">
                        <input type="password" id="password1" class="form-control" />
                        <label class="form-label" for="password1">Password</label>
                      </div>
                    </div> 
                    <div class="d-flex flex-row align-items-center mb-4">
                      <i class="fas fa-lock fa-lg me-3 fa-fw"></i>
                      <div class="form-outline flex-fill mb-0">
                        <input type="password" id="password2" class="form-control" />
                        <label class="form-label" for="password2">Re Password</label>
                      </div>
                    </div>
                    <div class="d-flex justify-content-center mx-4 mb-3 mb-lg-4">
                      <button type="button" class="btn btn-success text-white text-decoration-none" 
                          on:click={RegisterApi}>
                          Register
                      </button>
                  </div>
                  </form>
  
                </div>
                <div class="col-md-10 col-lg-6 col-xl-7 d-flex align-items-center order-1 order-lg-2">
                    <img src="../../register.webp" class="img-fluid" alt="Registerimage" />
                </div>
                <small class="text-center text-muted">Please write your password to confirm your registration.</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Modal message = "Please make sure that you entered a valid data."/>
</section>