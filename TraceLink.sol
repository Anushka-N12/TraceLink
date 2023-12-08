//SPDX-License_Identifier: MIT (open-source)
pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract TraceLink {
    //state variables
    mapping(uint => Product) public Pmap;
    uint public PmapSize = 0;
    mapping(uint => Company) public Cmap;
    uint public CmapSize = 0;
    // Product[] public Product_arr;
    // Company[] public Company_arr;
    uint current_pid;

    struct Product {
        uint PId;
        string PName;
        string Brand;
        uint PQuant;
        uint[] clicks;
        SCSection[] SChain;
    }

    struct Company {
        uint CId;
        string CName;
        string CType;
        uint[] CProducts;
    }

    struct SCSection {
        uint ProductId;
        uint FromId;
        uint ToId;
        string EmpId;
        string Task;
        string Location;
        uint TimeRecieved;
        uint TimeOfHandOver;
    }

    //Function or TRANSACTION that updates the product array
    //Company Id here will be picked up during login time
    //Timestamps will be converted to readable format in python
    function StoreProduct(
        uint CompanyId,
        string memory ProductName,
        string memory PBrand,
        uint quant,
        uint FId,
        uint To_Id,
        string memory EmployeeId,
        string memory TaskDetails,
        string memory Current_Location
    ) public returns (uint ProductId) {
        ProductId = PmapSize + 1;
        Product storage p = Pmap[ProductId];
        p.PId = ProductId;
        p.PName = ProductName;
        p.Brand = PBrand;
        p.PQuant = quant;
        for (uint256 i = 0; i < quant; i++) {
            p.clicks.push(0);
        }
        p.SChain.push(
            SCSection(
                PmapSize + 1,
                FId,
                To_Id,
                EmployeeId,
                TaskDetails,
                Current_Location,
                block.timestamp,
                block.timestamp
            )
        );
        PmapSize += 1;
        Cmap[CompanyId].CProducts.push(ProductId);
        return ProductId;
    }

    //The PMap doesn't directly show me the SChain when I run transactions in the Remix sidebar,
    // so I just wrote another function to get them explicitly.
    // function showsc(uint pid) public view returns(SCSection[] memory sc){sc = Pmap[pid].SChain;}

    //Show function to call externally
    function showPDetails() public view returns (Product memory p) {
        p = Pmap[current_pid];
        return p;
    }

    //function to update count, to be called by above showPDetails function
    function updateCount(uint pid, uint piece_num) public {
        Product storage p = Pmap[pid];
        p.clicks[piece_num - 1] += 1;
        current_pid = pid;
    }

    //Function or TRANSACTION that updates the supply chain of a product
    //It allows only the company that is currently handling the product to add data
    // *FId below must be taken automatically after user logs in
    function StoreSCS(
        uint Product_Id,
        uint FId,
        uint To_Id,
        string memory EmployeeId,
        string memory TaskDetails,
        string memory Current_Location
    ) public {
        SCSection[] memory chain = Pmap[Product_Id].SChain;
        uint lastC = chain[chain.length - 1].ToId;
        if (lastC == FId) {
            Pmap[Product_Id].SChain.push(
                SCSection(
                    Product_Id,
                    FId,
                    To_Id,
                    EmployeeId,
                    TaskDetails,
                    Current_Location,
                    block.timestamp,
                    block.timestamp
                )
            );
        }
    }

    //*Company will be notified whenever any information is added to their product to ensure their awareness of the process

    function addCompany(
        string memory Name,
        string memory CompanyType
    ) public returns (uint CompanyId) {
        CompanyId = CmapSize + 1;
        Company storage c = Cmap[CompanyId];
        c.CId = CompanyId;
        c.CName = Name;
        c.CType = CompanyType;
        CmapSize += 1;
        return CompanyId;
    }

    constructor() public {
        addCompany("Gucci", "Luxury Fashion");
        addCompany("Globalx", "Logistics");
        addCompany("Barari", "Olive Oil Manufacturing");
        addCompany("Madina", "Hypermarket Francise");
        StoreProduct(
            1,
            "Bag",
            "Gucci",
            50,
            1,
            1,
            "df ht",
            "rbth5ytn",
            "wrhetrytjh"
        );
    }
}
