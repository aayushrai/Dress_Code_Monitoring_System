import React, { useEffect, useState } from 'react'
import Button from '@material-ui/core/Button';
import {useHistory } from "react-router-dom";


import './Enroll.css';


const url = "http://127.0.0.1:8000";

function Enroll() {

    const history = useHistory();
    const [user,setUser] = useState({"user_name":"","user_phone":"","user_address":"","user_email":""});
    const addUser = ()=> {
        const requestOptions = {    
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(user)
            };
        fetch(url+'/adduser', requestOptions)
        .then(response => response.json())
        .then(data => {
            history.push("/productselect/"+data["user_id"]);
        })}
      
    return (
        <div className="checkout">
            <div className="person__data">
                <div className="person__image">
                
                <img src={url+"/media/detectedFace/face.jpg"}></img>
                </div>
                <div className="person__info">
                    
                    <div className="lineone">
                        <div>
                            <label className="label">Customer Name</label>
                            <br></br>
                            <input type="text" id="fname" name="firstname" size= "40" value={user.user_name} onChange={e => setUser({...user,"user_name":e.target.value})} ></input>
                        </div>
                    </div>
                    <div className="linetwo">
                        <div>
                            <label className="label">Contact</label>
                            <br></br>
                            <input type="text" id="contact" name="contact" value={user.user_phone} onChange={e => setUser({...user,"user_phone":e.target.value})}   ></input>
                        </div>
                        
                    </div>
                    <div className="linethree">
                        <label className="label">Address</label>
                        <br></br>
                        <input size="53" type="text" id="address" name="address" value={user.user_address} onChange={e => setUser({...user,"user_address":e.target.value})}   ></input>
                    </div>
                    <div className="linethree">
                        <label className="label">Email</label>
                        <br></br>
                        <input size="53" type="text" id="email" name="email" value={user.user_email} onChange={e => setUser({...user,"user_email":e.target.value})}  ></input>
                    </div>
                </div>
            </div>
            <div className="btn_enroll">
                    <Button variant="contained" color="primary" onClick={() => {addUser()}} >
                        Enroll Customer
                    </Button>
                </div>
        </div>
    )
}

export default Enroll
