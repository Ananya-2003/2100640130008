// src/components/ProductDetail.jsx
import React, { useState, useEffect } from 'react';
import { Typography, Card, CardContent, CardMedia, Button } from '@mui/material';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const ProductDetail = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    fetchProduct();
  }, [id]);

  const fetchProduct = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/categories/Laptop/products/${id}`);
      setProduct(response.data);
    } catch (error) {
      console.error("Error fetching product data:", error);
    }
  };

  if (!product) return <Typography>Loading...</Typography>;

  return (
    <div>
      <Typography variant="h4">{product.productName}</Typography>
      <Card>
        <CardMedia
          component="img"
          height="300"
          image={`https://via.placeholder.com/300?text=${product.productName}`}
          alt={product.productName}
        />
        <CardContent>
          <Typography>Company: {product.company}</Typography>
          <Typography>Category: {product.category}</Typography>
          <Typography>Price: ${product.price}</Typography>
          <Typography>Rating: {product.rating}</Typography>
          <Typography>Discount: {product.discount}%</Typography>
          <Typography>Availability: {product.availability}</Typography>
        </CardContent>
      </Card>
      <Button href="/">Back to List</Button>
    </div>
  );
};

export default ProductDetail;

