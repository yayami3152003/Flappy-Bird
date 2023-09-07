<?php

class Product
{
    public $ID;
    public $Name;
    public $Price;
}

class Store
{
    public $Products;

    public function __construct()
    {
        $this->Products = array();
    }

    public function AddProduct($p)
    {
        $this->Products[] = $p;
    }

    public function RemoveProductByID($id)
    {
        foreach ($this->Products as $key => $p) {
            if ($p->ID == $id) {
                unset($this->Products[$key]);
                return;
            }
        }
    }

    public function GetProductByID($id)
    {
        foreach ($this->Products as $p) {
            if ($p->ID == $id) {
                return $p;
            }
        }
        return null;
    }

    public function GetProducts()
    {
        return $this->Products;
    }

    public function SaveToDatabase($host, $username, $password, $database)
    {
        $conn = mysqli_connect($host, $username, $password, $database);
        if (!$conn) {
            die("Lỗi kết nối tới cơ sở dữ liệu: " . mysqli_connect_error());
        }

        $sql = "CREATE TABLE IF NOT EXISTS products (
            id INT(11) AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price FLOAT
        )";
        mysqli_query($conn, $sql);

        foreach ($this->Products as $p) {
            $name = mysqli_real_escape_string($conn, $p->Name);
            $price = $p->Price;
            $sql = "INSERT INTO products (name, price) VALUES ('$name', $price)";
            mysqli_query($conn, $sql);
        }

        mysqli_close($conn);
    }

    public static function LoadFromDatabase($host, $username, $password, $database)
    {
        $conn = mysqli_connect($host, $username, $password, $database);
        if (!$conn) {
            die("Lỗi kết nối tới cơ sở dữ liệu: " . mysqli_connect_error());
        }

        $store = new Store();
        $sql = "SELECT * FROM products";
        $result = mysqli_query($conn, $sql);

        while ($row = mysqli_fetch_assoc($result)) {
            $p = new Product();
            $p->ID = $row['id'];
            $p->Name = $row['name'];
            $p->Price = $row['price'];
            $store->AddProduct($p);
        }

        mysqli_close($conn);
        return $store;
    }
}

$store = new Store();

// Thêm sản phẩm vào cửa hàng
$product1 = new Product();
$product1->ID = 1;
$product1->Name = "iPhone 13";
$product1->Price = 1000;
$store->AddProduct($product1);

$product2 = new Product();
$product2->ID = 2;
$product2->Name = "Samsung Galaxy S21";
$product2->Price = 900;
$store->AddProduct($product2);

// Lưu cửa hàng vào cơ sở dữ liệu
$host = "localhost";
$username = "root";
$password = "";
$database = "store_database";