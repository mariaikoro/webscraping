import React from 'react';
import SearchBar from './components/SearchBar';
import ItemList from './components/ItemList';
import db from "./firebase";

//to limit reads from database, may need to update item object
// give a normal ingredients array
// give normal brand name
// this will make retrieval and displaying on component easier

class App extends React.Component {

    state = { items: []}

    onSearchSubmit= async (term) => {
        const ingredientsRef = db.collection('ingredients');
        var snapshot = await ingredientsRef.where('name', '==', term).get();
        if (snapshot.empty) {
        console.log('No matching documents.');
        return;
        }  

        var id = snapshot.docs.pop(0).id
        //console.log(id)

        const itemsRef = db.collection('items');
        snapshot = await itemsRef.where("ingredients",'array-contains',id).get();
        if (snapshot.empty) {
            console.log('No matching documents.');
            return;
            }

        let arr = snapshot.docs.map((doc) => {
            return doc = doc.data();
        })

        this.setState({ items : arr})

    }

    render() {
        return (
            <div className = "ui container" style = {{ marginTop: '10px'}}>
                <SearchBar onSubmit = {this.onSearchSubmit} />
                Found {this.state.items.length} items
                <ItemList items = {this.state.items} />
            </div>
        )
    }
}

export default App;