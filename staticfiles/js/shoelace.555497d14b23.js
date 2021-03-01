<script>
  (() => {
    const drawer = document.querySelector('.drawer-placement-left');
    const openButton = drawer.nextElementSibling;
    const closeButton = drawer.querySelector('sl-button[type="primary"]');

    openButton.addEventListener('click', () => drawer.show());
    closeButton.addEventListener('click', () => drawer.hide());
  })();
</script>