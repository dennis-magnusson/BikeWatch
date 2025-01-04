import FormInput from "./FormInput";
import KeywordAdder from "./KeywordAdder";
import MinMaxInput from "./MinMaxInput";
import SearchableMultiselect from "./SearchableMultiselect";
import { Button } from "./ui/button";
import { Label } from "./ui/label";

function FilterForm() {
    return (
        <>
            <div
                style={{
                    display: "flex",
                    flexDirection: "column",
                    minWidth: "280px",
                }}
            >
                <FormInput>
                    <Label htmlFor="city">Location</Label>
                    <SearchableMultiselect />
                </FormInput>

                <FormInput>
                    <Label htmlFor="">Price</Label>
                    <MinMaxInput unit="€" />
                </FormInput>
                {/* <FormInput>
                    <Label htmlFor="">Model year</Label>
                    <MinMaxInput unit="" />
                </FormInput> */}

                <FormInput>
                    <Label htmlFor="Custom keywords">Custom keywords</Label>
                    <KeywordAdder />
                </FormInput>

                <FormInput>
                    <Button>Update filters</Button>
                </FormInput>
            </div>
        </>
    );
}

export default FilterForm;
