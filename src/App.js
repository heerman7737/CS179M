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
                    {/*<Route path="/ComponentList" element={<ComponentList/>}/>*/}
                    {/*<Route path="/FailmodeList" element={<FailmodeList/>}/>*/}
                    {/*<Route path="/MappingList" element={<MappingList/>}/>*/}

                    {/* Using path="*"" means "match anything", so this route
                    acts like a catch-all for URLs that we don't have explicit
                    routes for. */}
                    </Route>

                </Routes>
            </BrowserRouter>
        </div>
    );
}

function IndexPage() {
    return (
        <div>
            {/* A "layout route" is a good place to put markup you want to
          share across all the pages on your site, like navigation. */}
            {/*<nav>*/}
            {/*    <ul>*/}
            {/*        <li>*/}
            {/*            <Link to="/">Home</Link>*/}
            {/*        </li>*/}
            {/*        <li>*/}
            {/*            <Link to="/components">Components</Link>*/}
            {/*        </li>*/}
            {/*        <li>*/}
            {/*            <Link to="/failmodes">Fail Modes</Link>*/}
            {/*        </li>*/}
            {/*        <li>*/}
            {/*            <Link to="/mappings">Mappings</Link>*/}
            {/*        </li>*/}
            {/*        /!*<li>*!/*/}
            {/*        /!*  <Link to="/nothing-here">Nothing Here</Link>*!/*/}
            {/*        /!*</li>*!/*/}
            {/*    </ul>*/}
            {/*</nav>*/}


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
