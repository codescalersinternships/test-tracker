
<script>
    import axios from '../healpers/axios'
    import Button from "../components/ui/Button.svelte";
    import Modal from "../components/ui/Modal.svelte";


    async function loginApi(){
        const data = {
            email: document.getElementById('email').value,
            password: document.getElementById('password').value
        }
        try {
            const response = await axios.post('/auth/login/', data)
            if (response.status === 200) { 
                const token = response.data.access_token
                localStorage.setItem("token", token)
                window.location.href = '/'
            }
        } 
        catch(err) {
            document.querySelector('.modal').style.display = 'block'
        }
    }

</script>

<section class="vh-100">
    <div class="container py-5 h-100">
    <div class="row d-flex align-items-center justify-content-center h-100">
        <div class="col-md-8 col-lg-7 col-xl-6">
        <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.svg"
            class="img-fluid" alt="Phoneimage">
        </div>
        <div class="col-md-7 col-lg-5 col-xl-5 offset-xl-1">
            <form>
                <div class="pb-4">
                    <p class="h5">
                        We were missing you!
                    </p>
                </div>
                <!-- Email input -->
                <div class="form-outline mb-4">
                    <input type="email" id="email" class="form-control form-control-lg" />
                    <label class="form-label" for="email">Email</label>
                </div>
                <!-- Password input -->
                <div class="form-outline mb-4">
                    <input type="password" id="password" class="form-control form-control-lg" />
                    <label class="form-label" for="password">Password</label>
                </div>
                <!-- Submit button -->
                <div class="d-flex justify-content-center mx-4 mb-3 mb-lg-4">
                    <Button Class="btn btn-primary btn-lg" Function={loginApi} text="Login" />
                </div>
            </form>
        </div>
    </div>
    </div>
    <Modal message = "Please make sure that you enter the correct email and password."/>
</section>
