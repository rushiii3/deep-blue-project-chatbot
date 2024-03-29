import { lazy } from "react";
function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
const LandingPage = lazy(() =>
  wait(1000).then(() => import("./Pages/LandingPage"))
);

const Login = lazy(() =>
wait(1000).then(() => import("./Pages/LoginPage"))
); 
const UploadPage = lazy(() =>
wait(1000).then(() => import("./Pages/UploadPage"))
); 

const AddPdfPage = lazy(() =>
wait(1000).then(() => import("./Pages/AddPdfPage"))
); 
export { LandingPage, Login, UploadPage, AddPdfPage};
