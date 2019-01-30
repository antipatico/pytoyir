#!/usr/bin/env python3
import whoosh.lang.porter as porter
import whoosh.lang.porter2 as porter2
import whoosh.lang.paicehusk as paicehusk

if __name__ == "__main__":
	print(porter.stem("dancer"))
	print(porter2.stem("dancer"))
	print(paicehusk.stem("dancer"))
