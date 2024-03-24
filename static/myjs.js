
        // Lắng nghe sự kiện submit của biểu mẫu
        document.getElementById("productForm").addEventListener("submit", function(event) {
            event.preventDefault(); // Ngăn chặn hành động mặc định của form

            // Lấy giá trị từ các trường input
            var name = document.getElementById("name").value;
            var price = document.getElementById("price").value;
            var number = document.getElementById("number").value;

            // Tạo một đối tượng FormData chứa dữ liệu
            var formData = new FormData();
            formData.append("name", name);
            formData.append("price", price);
            formData.append("number", number);

            // Gửi yêu cầu POST đến route '/add' với dữ liệu từ biểu mẫu
            fetch("/add", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                //alert(data.message); // In ra thông báo từ server
                //location.reload(); // Tải lại trang sau khi thêm sản phẩm thành công
            })
            .catch(error => console.error("Error:", error));
        });


        document.addEventListener('DOMContentLoaded', function() {
            var deleteButtons = document.querySelectorAll('.delete-btn');
            deleteButtons.forEach(function(button) {
                button.addEventListener('click', function() {
                    var productId = this.getAttribute('data-product-id');
                    var confirmation = confirm('Are you sure you want to delete this product ?');
                    if (confirmation) {
                        // gửi yêu cầu DELETE đến route '/delete' với dữ liệu xóa là id sản phẩm
                        fetch('/delete/' + productId, {
                            method: 'DELETE',
                        })
                        .then(response => {
                            if (response.ok) {
                                // Xóa sản phẩm khỏi DOM
                                var row = this.closest('tr');
                                row.remove();
                                return response.json();
                            }
                            throw new Error('Product delete failure');
                            // in ra alert cho biết thành công
                        })
                        .then(data => {
                            alert(data.message);
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            alert('Failed to delete product, an error ocurred');
                        });
                    }
                });
            });
        });


        
        var editModal = document.getElementById("myModal")
        function setProductInfo(id,name,price){
            var productIdInput = document.getElementById("modal-productID");
            var productNameInput = document.getElementById("modal-productName");
            var productPriceInput = document.getElementById("modal-productPrice");
        
            productIdInput.value = id;
            productNameInput.value = name;
            productPriceInput.value = price;
        }

        document.addEventListener('DOMContentLoaded', function() {
            var fixButtons = document.querySelectorAll(".edit-btn");
            fixButtons.forEach(function(button) {
                button.addEventListener('click', function() {
                    var row = this.closest('tr');
                    var productID = row.querySelector('.productID').textContent; // Lấy dữ liệu từ thẻ có class là productID
                    var productName = row.querySelector('.productInfo').textContent; // Lấy dữ liệu từ thẻ có class là productInfo
                    var productPrice = row.querySelector('.unitPrice').textContent; // Lấy dữ liệu từ thẻ có class là unitPrice
                    editModal.style.display = "block";
                    // Hiển thị thông tin của sản phẩm
                    setProductInfo(productID, productName, productPrice);
                })

            })
        })

        window.onclick = function(event) {
            if (event.target == editModal){
                editModal.style.display = "none";
          }
        }

        var span = document.getElementsByClassName("closeEdit")[0];
        span.onclick = function() {
            editModal.style.display = "none";
        }

        confirmButton = document.getElementById("confirm-btn")
        confirmButton.addEventListener('click', function(){
            editModal.style.display = "none";
        })