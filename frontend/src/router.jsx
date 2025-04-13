import { BrowserRouter, Routes, Route } from 'react-router-dom';

import { LandingScreen } from "./pages/LandingScreen";


function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<LandingScreen />} />
            </Routes>
        </BrowserRouter>
    );
}


export default AppRouter;