import React from 'react';
import Item from './Item';

const ItemList  = (props) => {
   
    const items = props.items.map((item) => {
        //should create an item component and return as item component here
        return <Item key = {item.name} itemName = {item.name} brandName = {item.brandID} ingredients = {item.ingredients} />
    })
    return (
        <div>
            {items}
        </div>
    )
}

export default ItemList;