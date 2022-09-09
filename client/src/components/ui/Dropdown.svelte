<script>
    import DropDownSVG from "../svg/DropDownSVG.svelte"
</script>

<!-- Pass the dropdown links -->
<div class="dropdown dropdowncustom p-1">
    <a
        class="dropdown-toggle"
        id="dropdownMenuButton"
        data-mdb-toggle="dropdown"
        aria-expanded="false"
        >
        <DropDownSVG />
    </a>
    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
        <li>
            <slot></slot>
        </li>
    </ul>
</div>