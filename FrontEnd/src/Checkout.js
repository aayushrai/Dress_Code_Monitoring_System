import Table from './ProductsCheckout';
import Button from '@material-ui/core/Button';
import React, { useState } from 'react';
import "./Checkout.css";
import {
    useParams,
    useHistory
  } from "react-router-dom";
import { useEffect } from 'react';
const url = "http://127.0.0.1:8000";
function Checkout() {
    const [OrderData,setOrder] = useState([]);
    const params = useParams();
    const history = useHistory();
    const [Discount,setDiscount] = useState(0);
    useEffect(() => {
        fetch(url+'/order/'+ params.order_id)
              .then((response) => {
               //  console.log(response.json());
                return response.json();
               })
               .then((data)=>{
                 setOrder(data);
                 if((data[0].order_count)%10===0){
                 setDiscount(parseInt(params.total*(0.05)));
                 }
                // console.log("order",data);
               });
               OrderData.map((item)=>{
            })
  
        }, [])

        const sendbill = ()=> {
            const requestOptions = {    
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({"order_id":params.order_id})
                };
            fetch(url+'/sendbill', requestOptions)
            .then(response => response.json())
            .then(data => {
                history.push("/");
            })}
       
        
    return (
        <div className="checkout">
            <div className="person__data">
                <div className="person__image">
                    <img src={OrderData.length &&  url+OrderData[0].user_image} />
                </div>
                <div className="person__info">
                    <div className="lineone">
                        <div>
                            <label className="label">Order Id</label>
                            <br></br>
                            <input type="text" id="orderid" name="Order" value={params.order_id} size="33" readOnly></input>
                        </div>
                        <div>
                            <label className="label">Total Number Of Orders</label>
                            <br></br>
                            <input type="text" id="orderCount" name="Order" value={OrderData.length && OrderData[0].order_count} size="33" readOnly></input>
                        </div>
                    </div>
                    <div className="lineone">
                        <div>
                            <label className="label">Customer Name</label>
                            <br></br>
                            <input type="text" id="fname" name="firstname" value={OrderData.length &&  OrderData[0].user_name} size="33" ></input>
                        </div>
                        <div>
                            <label className="label">Customer Email</label>
                            <br></br>
                            <input type="text" id="email" name="firstname" value={OrderData.length &&  OrderData[0].user_email} size="33" ></input>
                        </div>
                    </div>
                    <div className="linetwo">
                        <div>
                            <label className="label">Contact</label>
                            <br></br>
                            <input type="text" id="contact" name="contact" value={OrderData.length &&  OrderData[0].user_phone} size="33" ></input>
                        </div>
                        <div>
                            <label className="label">Payment Method</label>
                            <br></br>
                            <select name="payment" id="payment">
                                <option value="cash">Cash</option>
                                <option value="card">Card</option>
                                <option value="wallet">Online Wallet</option>
                                <option value="Scan">Scan and pay</option>
                            </select>
                        </div>
                    </div>
                    <div className="linethree">
                        <label className="label">Address</label>
                        <br></br>
                        <input size="75" type="text" id="address" name="address" value={OrderData.length &&  OrderData[0].user_address} ></input>
                    </div>
                    <div className="linefour">
                        <div >
                            <label className="label">Number Of Items</label>
                            <br></br>
                            <input type="text" id="items" name="items" value={OrderData.length -1} ></input>
                        </div>
                        <div>
                            <label className="label">Orignal Price</label>
                            <br></br>
                            <input type="text" id="price" name="price" value={params.total} ></input>
                        </div>
                    </div>
                    <div className="linefour">
                        <div >
                            <label className="label">Discount</label>
                            <br></br>
                            <input type="text" id="items" name="items" value={Discount} ></input>
                        </div>
                        <div>
                            <label className="label">Final Price</label>
                            <br></br>
                            <input type="text" id="price" name="price" value={(params.total)-Discount} ></input>
                        </div>
                    </div>
                </div>
                <div>
                    <Button variant="contained" color="black" onClick={()=>{sendbill()}}>
                        Order Now
                    </Button>
                </div>
            </div>
            {OrderData.length > 0 &&
                <Table order={OrderData}/>
                 }
        
        </div>
    )
}

export default Checkout;
