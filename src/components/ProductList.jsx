// src/components/ProductList.js
import React, { useState, useEffect } from 'react';
import { Typography, TextField, Button, Grid, Card, CardContent, CardMedia } from '@mui/material';
import axios from 'axios';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [filters, setFilters] = useState({ category: '', company: '', rating: '', minPrice: '', maxPrice: '', availability: '' });
  const [sort, setSort] = useState('price');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchProducts();
  }, [filters, sort, page]);

  const fetchProducts = async () => {
    const { category, company, rating, minPrice, maxPrice, availability } = filters;
    const response = await axios.get(`http://localhost:5000/categories/Laptop/products`, {
      params: {
        n: 10,
        page: page,
        category,
        company,
        rating,
        minPrice,
        maxPrice,
        availability,
        sort
      }
    });
    setProducts(response.data.products);
    setTotalPages(response.data.totalPages);
  };

  const handleFilterChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  return (
    <div>
      <Typography variant="h4">Product List</Typography>
      <TextField label="Category" name="category" onChange={handleFilterChange} />
      <TextField label="Company" name="company" onChange={handleFilterChange} />
      <TextField label="Rating" name="rating" onChange={handleFilterChange} />
      <TextField label="Min Price" name="minPrice" type="number" onChange={handleFilterChange} />
      <TextField label="Max Price" name="maxPrice" type="number" onChange={handleFilterChange} />
      <TextField label="Availability" name="availability" onChange={handleFilterChange} />
      <Button onClick={() => setSort(sort === 'price' ? 'rating' : 'price')}>Sort by {sort === 'price' ? 'Rating' : 'Price'}</Button>
      <Grid container spacing={2}>
        {products.map(product => (
          <Grid item xs={12} sm={6} md={4} key={product.id}>
            <Card>
              <CardMedia
                component="img"
                height="140"
                image={`https://via.placeholder.com/150?text=${product.productName}`}
                alt={product.productName}
              />
              <CardContent>
                <Typography variant="h6">{product.productName}</Typography>
                <Typography>Price: ${product.price}</Typography>
                <Typography>Rating: {product.rating}</Typography>
                <Typography>Discount: {product.discount}%</Typography>
                <Typography>Availability: {product.availability}</Typography>
                <Button href={`/product/${product.id}`}>View Details</Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
      <Button onClick={() => setPage(prev => Math.max(prev - 1, 1))}>Previous</Button>
      <Button onClick={() => setPage(prev => Math.min(prev + 1, totalPages))}>Next</Button>
    </div>
  );
};

export default ProductList;
