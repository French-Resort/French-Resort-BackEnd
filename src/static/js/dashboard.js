$(document).ready( function () {
    $('#dataTable').DataTable();

    $('.cancel-btn').click(function() {
        const bookingId = $(this).data('id');

        if(confirm("Are you sure you want to cancel this booking?")) {
            $.ajax({
                url: "{{urlfor('url_for('update_booking', id_booking=booking.id_booking ')}}",
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ booking_id: bookingId }),
                success: function(response) {
                    // Remove the booking row from the table
                    $('#booking-' + bookingId).remove();
                    alert(response.message); // Or use a more sophisticated method to notify the user
                },
                error: function(xhr, status, error) {
                    console.error("Error: " + error);
                    alert("An error occurred while canceling the booking.");
                }
            });
        }
    });
} );