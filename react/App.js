import logo from './logo.svg';
import './App.css';
import {Routes, Route, BrowserRouter, Outlet} from "react-router-dom";
import LoginForm from "./components/login";
import FileUpload from "./components/uploadManifest";

function App() {
  return (
        <div className="App">
            <h1>179M Project</h1>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<IndexPage/>}>
                        <Route path="/login" element={<LoginForm />} />
                        <Route path="/uploadManifest" element={<FileUpload />} />
                        {/*<Route path="/operate" element={<MappingList />} />*/}

                    </Route>

                </Routes>
            </BrowserRouter>
        </div>
    );
}

function IndexPage() {
    return (
        <div>


            {/*<PersistentDrawerLeft/>*/}

            <hr/>

            {/* An <Outlet> renders whatever child route is currently active,
          so you can think about this <Outlet> as a placeholder for
          the child routes we defined above. */}
            <Outlet/>
        </div>
    );
}

export default App;
