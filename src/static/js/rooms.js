$(document).ready( function () {
    $('#dataTable').DataTable();

    $('#dataTable').on('click', '.delete-btn', function() {
        const roomId = $(this).data('id');
        const row = $(this).closest('tr');

        if(confirm("Are you sure you want to delete this room?")) {
            $.ajax({
                url: `/api/room/${roomId}`,
                method: 'DELETE',
                contentType: 'application/json',
                success: function(response) {
                    alert(`Room ${roomId} removed!`);
                    $('#dataTable').DataTable().row(row).remove().draw(false);
                },
                error: function(xhr, status, error) {
                    console.error("Error: " + error);
                    alert(`An error occurred while canceling the room !. The room may be referenced to booking table !`);
                }
            });
        }
    });
} );