<script>
    export let id;
</script>

<div class="col-12">
    <div class="card test_case_card">
        <div class="card test_case_card">
            <a data-mdb-toggle="collapse"
                href="#collapse-{id}"
                role="button"
                aria-expanded="false"
                aria-controls="collapse-{id}"
            >
                <slot name="collapse-dropdown" />
                <slot name="collapse-title"/>
            </a>

            <div class="test_case_info">
                <a
                    class="collapse_span"
                    data-mdb-toggle="collapse"
                    href="#collapse-{id}"
                    role="button"
                    aria-expanded="false"
                    aria-controls="collapse-{id}"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="25"
                        height="30"
                        fill="currentColor"
                        class="bi bi-chevron-compact-down"
                        viewBox="0 0 16 16"
                    >
                        <path
                            fill-rule="evenodd"
                            d="M1.553 6.776a.5.5 0 0 1 .67-.223L8 9.44l5.776-2.888a.5.5 0 1 1 .448.894l-6 3a.5.5 0 0 1-.448 0l-6-3a.5.5 0 0 1-.223-.67z"
                        />
                    </svg>
                </a>
                <slot name="collapse-body" />
            </div>
        </div>
    </div>
</div>

<svelte:head>
    <title>Test-Tracker | Test Suite Detail</title>
    <style>
        .title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #5a79b1;
        }
        ul {
            margin: 0;
        }
        h1 {
            font-size: 1.5rem;
        }
        h3 {
            font-size: 20px;
        }
        .card_info {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            padding: 20px;
            margin-bottom: 20px;
        }
        .card_info p {
            font-size: 20px;
            font-weight: 700;
        }

        .test_case_card {
            position: relative;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
        }
        .test_case_card a {
            text-decoration: none;
            color: #5a79b1;
            display: block;
            font-weight: 700;
        }
        .collapse_span {
            position: absolute;
            right: 30px;
            height: 30px;
            width: 30px;
            text-align: center;
            border-radius: 50%;
        }
        .test_case_info {
            margin-top: 10px;
            padding: 5px;
        }
        .collapse-style {
            margin-left: 25px;
            margin-top: 15px;
            margin-bottom: 20px;
        }
        .collapse-style a {
            display: inline;
            color: #5a79b1;
            font-size: 17px;
        }
        .dropdowncustom{
            position: absolute;
            font-size: 0;
            right: 0;
            top:20px
        }
    </style>
</svelte:head>
