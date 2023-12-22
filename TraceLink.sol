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
    uint current_fcid;
    uint current_tcid;

    struct Product {
        uint PId;
        string PName;
        string Brand;
        string Desc;
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
        uint TimeOfHandOver;
    }

    //Function or TRANSACTION that updates the product array
    //Company Id here will be picked up during login time
    //Timestamps will be converted to readable format in python
    function StoreProduct(
        uint CompanyId,
        string memory ProductName,
        string memory PBrand,
        string memory pdesc,
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
        p.Desc = pdesc;
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

    //Show functions to call externally
    function showC()
        public
        view
        returns (string memory fc, string memory tc)
    {
        fc = Cmap[current_fcid].CName;
        tc = Cmap[current_tcid].CName;
        return (fc, tc);
    }

    function updateCft(uint fcid, uint tcid) public {
        current_fcid = fcid;
        current_tcid = tcid;
    }

    function showPDetails() public view returns (Product memory p) {
        p = Pmap[current_pid];
        return p;
    }

    //function to update count, to be called with showPDetails function
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
        
        if ((lastC == FId)
        || (lastC == FId)) {
            Pmap[Product_Id].SChain.push(
                SCSection(
                    Product_Id,
                    FId,
                    To_Id,
                    EmployeeId,
                    TaskDetails,
                    Current_Location,
                    block.timestamp
                )
            );
        }
    }

    //*Company will be notified whenever any information is added to their product to ensure their awareness of the process

    function addCompany(
        string memory Name,
        string memory CompanyType
    ) public  {
        Company storage c = Cmap[CmapSize+1];
        c.CId = CmapSize+1;
        c.CName = Name;
        c.CType = CompanyType;
        CmapSize += 1;
    }

    constructor() public {
        addCompany("Gucci", "Luxury Fashion");
        addCompany("Globalx", "Logistics");
        addCompany("Barari", "Olive Oil Manufacturing");
        addCompany("Madina", "Hypermarket Francise");
        addCompany("Offer House Ent.", "We buy bulk from manufacturers & sell at our retail stores");
        addCompany("XiaXiozhi", "Cheap tech contractors");
        addCompany("Factory Express", "Contract factory");
        addCompany("AliBaba", "Large E-commerce store");
        StoreProduct(
            1,
            "GG Marmount Small Shoulder Bag",
            "Gucci",
            '2023 Winter Collection',
            50,
            1,
            1,
            "m00851749", //Automatically taken
            "Order given to our factory 112 in Ajman",
            "Al Sufouh, Dubai"  //Automatically taken
        );
        StoreSCS(
                    1,
                    1,
                    1,
                    'm00375638',
                    'Manufactured products handed over to our warehouse 065',
                    'Sreet 24, Ajman'
                );
        StoreSCS(
                    1,
                    1,
                    5,
                    'm003732439',
                    'Handed over to Offer House Ent. for retail sales',
                    'JLT, Dubai'
                );
        StoreProduct(
            6,
            "Weixi T 11",
            "XaXiozhi",
            '2023 Main Release',
            100,
            6,
            7,
            "xab3857x", //Automatically taken
            "Order given to outsourced factory Express in X province",
            "Shanghai, China"  //Automatically taken
        );
        StoreSCS(
                    2,
                    7,
                    8,
                    'dfjhb7777',
                    'Shipped to Alibaba warehouse 201',
                    'X Province, China'
                );
        addCompany("Iran Farmers' Union", "Saffron Farming Corporation");
        addCompany('Blackmores', 'Herb Packaging');
        StoreProduct(
            10,
            "Grade 1 Pure Saffron ",
            "Blackmores",
            'Negin & Sargol parts of stigma hand-picked',
            50,
            9,
            10,
            "12948738-435", //Automatically taken
            "Produce transporting to packaging venue",
            "Tehran, Iran"  //Automatically taken
        );
        StoreSCS(
                    3,
                    10,
                    2,
                    'm00375638',
                    'Exporting 5kg of produce ie. 50 pieces globally',
                    'Jebel Ali Port, Dubai'
                );
        StoreSCS(
                    3,
                    2,
                    4,
                    'm00375638',
                    '25kg given to Madina',
                    'Jebel Ali Port, Dubai'
                );
    }
}
