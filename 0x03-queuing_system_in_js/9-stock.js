const express = require('express');
const { resolve } = require('path');
const redis = require('redis');
const util = require('util');

// data
const listProducts = [
  {
    id: 1,
    name: 'Suitcase 250',
    price: 250,
    stock: 4
  },
  {
    id: 2,
    name: 'Suitcase 450',
    price: 100,
    stock: 10
  },
  {
    id: 3,
    name: 'Suitcase 650',
    price: 350,
    stock: 2
  },
  {
    id: 1,
    name: 'Suitcase 1050',
    price: 550,
    stock: 5
  }
];

/**
 * gets an item from an array of objects.
 * @param {*} id id of item to be returned 
 * @returns object
 */
function getItemById(id) {

  return new Promise((resolve, reject) => {
    const itemArray = listProducts.filter(item => item.id === id).map(item => {
      return {
        itemId: item.id,
        itemName: item.name,
        price: item.price,
        initialAvailableQuantity: item.stock
      }
    });
    return resolve(itemArray[0]);
  })

}


/**
 * servers and redis clent
 */
const app = express();
const redisClient = redis.createClient();

redisClient.on('error', error => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

redisClient.on('connect', () => {
  console.log('Redis client connected to the server');
});

/**
 * set in redis the stock of a product by its id
 * @param {*} itemId id of product
 * @param {*} stock available units of product
 */
function reserveStockById(itemId, stock) {
  redisClient.set(itemId, stock);
}

/**
 * gets the stock value of an item from redis
 * @param {*} itemId id of item
 * @returns 
 */
async function getCurrentReservedStockById(itemId) {
  const promisifiedRedisGet = util.promisify(redisClient.get).bind(redisClient);
  const reservedStock = promisifiedRedisGet(itemId);
  return reservedStock;
}

// SERVER ROUTES
app.get('/list_products', (req, res) => {
  const productsArray = listProducts.map(item => {
    return {
      itemId: item.id,
      itemName: item.name,
      price: item.price,
      initialAvailableQuantity: item.stock
    }
  });
  return res.status(200).json(productsArray);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);

  const product = await getItemById(itemId);
  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }
  const currentProductStock = await getCurrentReservedStockById(itemId);
  if (!currentProductStock) {
    return res.status(404).json({ status: 'Product not found' });
  }
  // Add/update new property
  product.currentQuantity = currentProductStock;
  return res.status(200).json(product);
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);

  const product = await getItemById(itemId);
  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  // check available stock
  if (product.initialAvailableQuantity <= 0) {
    return res.json({ status: 'Not enough stock available', itemId })
  }

  reserveStockById(itemId, 1);

  return res.json({ status: 'Reservation confirmed', itemId })
});

app.listen(1245, () => {
  console.log('app is listening on port 1245');
});

