<script>
  import 'bootstrap/dist/css/bootstrap.min.css';
  
  let tokenVal;
  let message = 'Loading...';
  
  async function makeTokenReq() {
    try {
      const response = await fetch('/api/protected', {
        headers: {
          'Authorization': `Bearer ${tokenVal}`
        }
      });
      const data = await response.json();
      message = data.message;
    } catch (err) {
      message = 'Error connecting to server';
    }
  }
</script>

<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header bg-primary text-white">
          <h1 class="h4">Svelte simple auth app</h1>
        </div>
        <div class="card-body">
          <input 
            type="text" 
            class="form-control" 
            id="tokenInput" 
            aria-describedby="tokenInputHelp"
            bind:value={tokenVal}
            placeholder="Enter a token"
          >
          <button 
            type="submit" 
            class="btn btn-primary mt-2"
            on:click={makeTokenReq}
          >
            Check validity
          </button>
          <br />
          <p class="card-text mt-1">{message}</p>
        </div>
      </div>
    </div>
  </div>
</div>