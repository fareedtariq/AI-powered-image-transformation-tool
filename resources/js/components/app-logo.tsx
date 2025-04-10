
export default function AppLogo() {
    return (
        <>
            <div className="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square items-center justify-center rounded-md">
                {/* <AppLogoIcon className="size-5 fill-current text-white dark:text-black" /> */}

                <img className='object-contain' src="/images/logo.jpg" alt="" />
            </div>
            {/* <div className="ml-1 grid flex-1 text-left text-sm">
                <span className="mb-0.5 truncate leading-none font-semibold">AI IMAGE TRANSFORM </span>
            </div> */}
        </>
    );
}
