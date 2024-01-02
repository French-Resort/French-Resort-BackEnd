$(document).ready( function () {
    $('#dataTable').DataTable();

    $('#dataTable').on('click', '.delete-btn', function() {
        const bookingId = $(this).data('id');
        const row = $(this).closest('tr');

        if(confirm("Are you sure you want to delete this booking?")) {
            $.ajax({
                url: `/api/booking/${bookingId}`,
                method: 'DELETE',
                contentType: 'application/json',
                success: function(response) {
                    alert(`Booking ${bookingId} removed!`);
                    $('#dataTable').DataTable().row(row).remove().draw(false);
                },
                error: function(xhr, status, error) {
                    console.error("Error: " + error);
                    alert("An error occurred while canceling the booking.");
                }
            });
        }
    });
} );