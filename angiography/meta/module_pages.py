def get_landing_pages(m):
    landing_pages = {"FindStenosis": fr"""
        # Find stenosis
        ## Module description 
        Locate the stenosis in the x-ray angiography image.
        Select the coordinates using interactive x and y slider. 
        {m.n_syllables} items were selected.

        ## Stenosis definition
        The authors of the ARCADE dataset, Popov et al., 2024, used the syntax score (Sianos et al, 2005), to define stenosis as >= 50% degree of constriction  in coronary arteries of at least 1.5 _mm_ diameter.
        """,
        
        "ChooseArteryBox": fr"""
        # Find artery
        ## Module description
        Locate the requested artery in the x-ray angiography image.
        Select the coordinates using interactive x and y slider. 
        {m.n_syllables} items were selected.

        ## Artery definitions 
        If you need a description, how the artery segment is defined, hover over the i) button!

        """,

        "ChooseArteryName": fr"""
        # Choose artery name
        ## Module description 
        Choose between 4 different options, which artery is shown in the x-ray angiography image.
        {m.n_syllables} items were selected.

        ## Artery definitions 
        If you need a description, how the artery segment is defined, hover over the i) button next to the artery name button!

        
        """,

        "RightOrLeft": fr"""
        # Right or left
        ## Module description 
        Choose whether right or left coronary artery is depicted predominantely in the image. 
        {m.n_syllables} items were selected.

        ## Angulations
        |artery|angulation|
        |:---|---:|
        | left coronary artery   | Left Anterior Oblique caudal view |
        | left coronary artery   | Right Anterior Oblique caudal view |
        | left coronary artery   | Postero-Anterior cranial view |
        | left coronary artery   | Right Anterior Oblique cranial view |
        | right coronary artery   | Left Anterior Oblique cranial view |
        | right coronary artery   | Right Anterior Oblique cranial view |

        """        
        }
    return landing_pages[m.module_name]