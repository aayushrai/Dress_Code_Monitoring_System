import React, { Component } from 'react';
import './ProductCheckout.css';

class Table extends Component {
   
   
   constructor(props) {
      super(props) //since we are extending class Table so we have to use super in order to override Component class constructor
      this.state = { //state is by default an object
         products:this.props.order
      }
   }
   
   renderTableData() {
    return this.state.products.map((order, index) => {
       return (
          <tr key={order.product_id}>
             <td>{order.title}</td>
             <td>{order.description}</td>
             <td>{order.product_quantity}</td>
             <td>{order.weight}</td>
             <td>{order.price}</td>
          </tr>
       )
    })
 }

 renderTableHeader() {
    
    let header = Object.keys({"Title":"","Description":"","Quantity":"","weight":"","price":""})
    return header.map((key, index) => {
       return <th key={index}>{key.toUpperCase()}</th>
    })
 }

 render() {
    return (
       <div>
          <h1 className='title'>Shopping cart</h1>
          <table className='products'>
             <tbody>
                <tr>{this.renderTableHeader()}</tr>
                {this.renderTableData()}
             </tbody>
          </table>
       </div>
    )
 }
   }
   export default Table;