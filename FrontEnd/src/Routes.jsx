import  {  lazy } from 'react';

const LandingPage = lazy(() => import('./Pages/LandingPage'));
const Login = lazy(() => import('./Pages/LoginPage'));
const UploadPage = lazy(() => import('./Pages/UploadPage'));

export {
    LandingPage,
    Login,
    UploadPage
};
