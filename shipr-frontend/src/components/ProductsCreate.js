import {Wrapper} from "./Wrapper";
import {useState} from "react";
import {useNavigate} from 'react-router-dom';

export const ProductsCreate = () => {
    const [name, setName] = useState('');
    const [price, setPrice] = useState('');
    const [stock, setStock] = useState('');
    const navigate = useNavigate();

    const submit = async e => {
        e.preventDefault();

        await fetch(`${process.env.REACT_APP_INVENTORY_SERVICE_URL}/products`, {
            method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({
                name, price, stock
            })
        });

        console.log(name, price, stock);

        await navigate(-1);
    }

    return <Wrapper>
        <form className="mt-3" onSubmit={submit}>
            <div className="form-floating pb-3">
                <input className="form-control" placeholder="Name"
                       onChange={e => setName(e.target.value)}
                />
                <label>Name</label>
            </div>

            <div className="form-floating pb-3">
                <input type="number" className="form-control" placeholder="Price"
                       onChange={e => setPrice(e.target.value)}
                />
                <label>Price</label>
            </div>

            <div className="form-floating pb-3">
                <input type="number" className="form-control" placeholder="Stock"
                       onChange={e => setStock(e.target.value)}
                />
                <label>Stock</label>
            </div>

            <button className="w-100 btn btn-lg btn-primary" type="submit">Submit</button>
        </form>
    </Wrapper>
}