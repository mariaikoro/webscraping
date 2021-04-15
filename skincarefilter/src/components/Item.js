import React from 'react';
import db from '../firebase';

class Item extends React.Component {
    constructor(props) {
        super(props)
        this.state = {loading: true, brand: null}
    }
    // need to format ingredients using props
    async componentDidMount() {
        const brandRef = db.collection('brands');
        var snapshot = await brandRef.doc(this.props.brandName).get();
        this.setState({loading: false, brand: snapshot.data().name});
    }
    render() {
        if(this.state.loading){
            return (
                <div style = {{ border: "blue 3px solid" }}>
                    loading
                </div>
                )
        }else {
        return(
            <div style = {{ border: "blue 3px solid" }}>
                <h1>{this.props.itemName}</h1>
                <h2>{this.state.brand}</h2>
            </div>
        )}}
    }

export default Item;