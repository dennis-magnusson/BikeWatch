type FormInputProps = {
    children: React.ReactNode;
};

function FormInput({ children }: FormInputProps) {
    return <div className="flex flex-col gap-3 py-2">{children}</div>;
}

export default FormInput;
