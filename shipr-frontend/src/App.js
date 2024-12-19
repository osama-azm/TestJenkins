import {Products} from "./components/Product";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import {ProductsCreate} from "./components/ProductsCreate";
import {Orders} from "./components/Order";

function App() {
    return <BrowserRouter>
        <Routes>
            <Route path="/" element={<Products/>}/>
            <Route path="/create" element={<ProductsCreate/>}/>
            <Route path="/orders" element={<Orders/>}/>
        </Routes>
    </BrowserRouter>;
}

export default App;