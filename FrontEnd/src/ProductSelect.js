import React, { useEffect, useState } from 'react';
import Button from '@material-ui/core/Button';
import './ProductSelect.css';
import {
    Link,
    useParams,useHistory
  } from "react-router-dom";

const url = "http://127.0.0.1:8000";



function ProductSelect() {
    const history = useHistory();
    const params = useParams();
    const [ProductData,setProduct] = useState([]);
    const [Total,setTotal] = useState(0);
    const [CartData,setCartData] = useState([]);
    const [Count,setCount] = useState({});
    useEffect(() => {
        
            fetch(url+'/productdata')
              .then((response) => {
               //  console.log(response.json());
                return response.json();
               })
               .then((data)=>{
                 setProduct(data);
                //  console.log(data);
               });
       
    }, [])
    const placeOrder = ()=> {
    const requestOptions = {    
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(CartData)
        };
    fetch(url+'/placeorder', requestOptions)
    .then(response => response.json())
    .then(data => {
        history.push("/checkout/"+data["order_id"] + "/" + Total);
    
    })}
  
    

    const addData = (item) => {
    
    

        const index = CartData.findIndex(
            (data) => data.product_id === item.product_id
          );
       
        if(index >= 0){
            CartData[index]["product_quantity"] += 1
            setCartData(CartData);
            
        }
        else{
            setCartData([...CartData,{"product_quantity":1,"user_id":params.uid,"product_id":item.product_id}])
        }
        setTotal(Total + item.price);
    }
    return (
        <div>
            <div className="checkout__btn">
                    <Button onClick={() => placeOrder()} variant="contained" color="black" >
                        Checkout
                    </Button>
                </div>
            <div className="user__id"><h2>User Id</h2><p>{params.uid}</p></div>
            {ProductData.map(function (item,i){
                return(
                <div className="post">
                    <img className="product__img" src={item.logo}></img>
                    <div className="product__desc">{item.description}</div>
                    <div className="product__qty">
                        <div>
                            <label>Select Quantity</label>
                            <br></br>
                            <input className="exis_qty" type="text" value={Count[item.product_id]}></input>
                        </div>
                        <div>
                            <label>Quantity Available</label>
                            <p className="available">{item.quantity}</p>
                        </div>
                        <div className="button__div">
                        <Button onClick={() => addData(item)} variant="contained" color="primary">
                            ADD
                        </Button>
                        </div>
                    </div>
                    
                </div>)
            })}
        </div>
    )
        
    }

export default ProductSelect
