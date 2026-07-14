import winreg


def walk_registry(path, depth=0):

    try:

        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            path
        )


        indent = "    " * depth

        print(indent + path)


        value_count = winreg.QueryInfoKey(key)[1]


        for i in range(value_count):

            try:

                name, value, _ = winreg.EnumValue(key, i)

                print(
                    indent,
                    "VALUE:",
                    name,
                    "=",
                    value
                )

            except:
                pass



        subkeys = winreg.QueryInfoKey(key)[0]


        for i in range(subkeys):

            child = winreg.EnumKey(key,i)


            walk_registry(

                path + "\\" + child,

                depth + 1

            )


    except Exception:

        pass



walk_registry(

r"SYSTEM\CurrentControlSet\Enum\USB"

)