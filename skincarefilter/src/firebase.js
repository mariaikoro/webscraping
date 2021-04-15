//import * as firebase from 'firebase';
import firebase from "firebase/app";

//import * as firebase from 'firebase';
import 'firebase/firestore';


// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const config = {
    apiKey: "AIzaSyC44Ab9o_i7PgsK8b7mtRi1KHeNmg1yh90",
    authDomain: "skincare-filter.firebaseapp.com",
    projectId: "skincare-filter",
    storageBucket: "skincare-filter.appspot.com",
    messagingSenderId: "632343667379",
    appId: "1:632343667379:web:1c2768131a5d128c5546c6",
    measurementId: "G-RN5Y1RLLYC"
  };
var firebaseApp; 
if (!firebase.apps.length) {
  firebaseApp = firebase.initializeApp(config);
} else if (!firebaseApp) {
  firebaseApp = firebase.app()
}

const db = firebaseApp.firestore();

//export default config;

export default db;