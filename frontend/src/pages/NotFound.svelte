<script>

    import Button from "../components/ui/Button.svelte"

    function homePage() {
        window.location.href = '/'
    }

</script>

<section>

  <div class="page-wrap d-flex flex-row align-items-center">
      <div class="container">
          <div class="row justify-content-center">
              <div class="col-md-12 text-center">
                  <span class="display-1 d-block">404</span>
                  <div class="mb-4 lead">The page you are looking for was not found.</div>
                  
                  <Button Class="btn btn-primary" text='Back to Home' Function={homePage} />
              </div>
          </div>
      </div>
  </div>
  
</section>


<svelte:head>
 <title>Not Found</title>
</svelte:head>