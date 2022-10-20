$("#btnExport").click(function (e) {
    window.open('data:application/vnd.ms-excel,' + $('#table-id').html());
    e.preventDefault();
});