import { PropsWithChildren } from 'react';
import { Slide, ToastContainer } from 'react-toastify';
import { BACKGROUND_COLOR, BACKGROUND_IMAGE } from '../../consts/app';

import DevInfo from '../DevInfo/DevInfo';
import Header from '../Header/Header';
import Socials from '../Socials/Socials';

import 'react-toastify/dist/ReactToastify.css';

export function UtxoLayout({ children }: PropsWithChildren) {
  return (
    <>
      {/* <div
        style={styles.container}
        id="app-content"
        className="min-w-screen relative flex h-full min-h-screen w-full flex-col justify-between"
      >
        <div className="mx-auto flex max-w-screen-xl grow items-center sm:px-4">
          <main className="my-4 flex w-full flex-1 items-center justify-center">{children}</main>
        </div>
        <DisclaimerFooter />
        <Footer />
      </div> */}
      <div
        style={styles.container}
        id="app-content"
        className="min-w-screen relative flex h-full min-h-screen w-full flex-col justify-between"
      >
        <Header />
        <div className="mx-auto flex page-wrapper grow items-center sm:px-4">
          <main className="my-4 w-full">{children}</main>
        </div>
        <Socials />
        <DevInfo />
      </div>
      <ToastContainer
        stacked
        className="orpheus-toast"
        position="top-right"
        autoClose={7500}
        hideProgressBar={false}
        rtl={false}
        pauseOnFocusLoss
        theme="dark"
        pauseOnHover
        transition={Slide}
      />
    </>
  );
}

const styles = {
  container: {
    backgroundColor: BACKGROUND_COLOR,
    backgroundImage: BACKGROUND_IMAGE,
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
  },
};
